create database ISMS;

use ISMS;

/* =========创建用户信息表============ */

create table userTable
(
    uID   int identity
        constraint useTable_pk
            primary key,
    uName varchar(20) not null,
    uPwd  varchar(20) not null,
    uType varchar(10) not null
)
go

exec sp_addextendedproperty 'MS_Description', '系统用户注册表', 'SCHEMA', 'dbo', 'TABLE', 'userTable'
go

exec sp_addextendedproperty 'MS_Description', '用户ID', 'SCHEMA', 'dbo', 'TABLE', 'userTable', 'COLUMN', 'uID'
go

exec sp_addextendedproperty 'MS_Description', '用户类型，“采购员”“仓管员”“销售员”中的一种', 'SCHEMA', 'dbo', 'TABLE', 'userTable',
     'COLUMN', 'uType'
go

alter table dbo.userTable
    add constraint check_uType
        check ((uType='仓管员') or (uType='销售员') or (uType='采购员'))
go

/* ===========创建用户登录日志表============== */

create table loginLog
(
    logID         int identity
        constraint loginLog_pk
            primary key,
    uID           int                        not null
        constraint loginLog_useTable_uID_fk
            references userTable,
    loginDatetime datetime default getdate() not null
)
go

exec sp_addextendedproperty 'MS_Description', '用户登录日志表', 'SCHEMA', 'dbo', 'TABLE', 'loginLog'
go

/* ===========创建采购员信息表============== */

create table purchaserTable
(
    pID int identity
        constraint purchaserTable_pk
            primary key,
    uID int not null
        constraint purchaserTable_useTable_uID_fk
            references userTable
)
go

exec sp_addextendedproperty 'MS_Description', '采购员信息表', 'SCHEMA', 'dbo', 'TABLE', 'purchaserTable'
go

/* ============创建仓管员信息表============= */

create table keeperTable
(
    kID int identity
        constraint keeperTable_pk
            primary key,
    uID int not null
        constraint keeperTable_useTable_uID_fk
            references userTable
)
go

exec sp_addextendedproperty 'MS_Description', '仓管员信息表', 'SCHEMA', 'dbo', 'TABLE', 'keeperTable'
go

/* ===========创建销售员信息表=========== */

create table salesmanTable
(
    sID int identity
        constraint salesmanTable_pk
            primary key,
    uID int not null
        constraint salesmanTable_useTable_uID_fk
            references userTable
)
go

exec sp_addextendedproperty 'MS_Description', '销售员信息表', 'SCHEMA', 'dbo', 'TABLE', 'salesmanTable'
go

/* ===========创建角色触发器=========== */


create trigger insert_role
    on userTable
    after insert
    as
    begin
        if (select uType from inserted)='采购员'
        begin
            insert into purchaserTable(uID)
            select uID from inserted
        end
        else
        begin
            if (select uType from inserted)='仓管员'
            begin
                insert into keeperTable(uID)
                select uid from inserted
            end
            else
            begin
                insert into salesmanTable(uID)
                select uid from inserted
            end
        end
    end
go

insert into userTable(uName,uPwd,uType) values('salesmanA','123456','销售员')
insert into userTable(uName,uPwd,uType) values('purchaserA','123456','采购员')
insert into userTable(uName,uPwd,uType) values('keeperA','123456','仓管员')
go

/* ===========创建采购明细单表============= */

create table purchaseOrder
(
    poID           int identity
        constraint purchaseOrder_pk
            primary key,
    pID            int                        not null
        constraint purchaseOrder_purchaserTable_pID_fk
            references purchaserTable,
    cName          nvarchar(255)               not null,
    sName          nvarchar(255)               not null,
    pUnitPrice     money                      not null,
    pQuantity      float                      not null,
    pMeasuringUnit nvarchar(10)                not null,
    poDatetime     datetime default getdate() not null
)
go

alter table purchaseOrder
    add isInWarehouse bit default 0 not null
go

exec sp_addextendedproperty 'MS_Description', '采购商品是否已入库，0表示未入库，默认为0', 'SCHEMA', 'dbo', 'TABLE', 'purchaseOrder',
     'COLUMN', 'isInWarehouse'
go

exec sp_addextendedproperty 'MS_Description', '采购明细单', 'SCHEMA', 'dbo', 'TABLE', 'purchaseOrder'
go

exec sp_addextendedproperty 'MS_Description', '采购单编号', 'SCHEMA', 'dbo', 'TABLE', 'purchaseOrder', 'COLUMN', 'poID'
go

exec sp_addextendedproperty 'MS_Description', '采购员编号', 'SCHEMA', 'dbo', 'TABLE', 'purchaseOrder', 'COLUMN', 'pID'
go

exec sp_addextendedproperty 'MS_Description', '采购商品的名称', 'SCHEMA', 'dbo', 'TABLE', 'purchaseOrder', 'COLUMN', 'cName'
go

exec sp_addextendedproperty 'MS_Description', '供应商名称', 'SCHEMA', 'dbo', 'TABLE', 'purchaseOrder', 'COLUMN', 'sName'
go

exec sp_addextendedproperty 'MS_Description', '采购商品的单价', 'SCHEMA', 'dbo', 'TABLE', 'purchaseOrder', 'COLUMN',
     'pUnitPrice'
go

exec sp_addextendedproperty 'MS_Description', '采购商品的数量', 'SCHEMA', 'dbo', 'TABLE', 'purchaseOrder', 'COLUMN',
     'pQuantity'
go

exec sp_addextendedproperty 'MS_Description', '采购商品的计量单位名称', 'SCHEMA', 'dbo', 'TABLE', 'purchaseOrder', 'COLUMN',
     'pMeasuringUnit'
go

exec sp_addextendedproperty 'MS_Description', '采购下单时间', 'SCHEMA', 'dbo', 'TABLE', 'purchaseOrder', 'COLUMN',
     'poDatetime'
go

/* ==========创建库存信息表=========== */

create table inventoryTable
(
    cID            int identity
        constraint inventoryTable_pk
            primary key,
    cName          nvarchar(255)               not null,
    cQuantity      float                      not null,
    updateDatetime datetime default getdate() not null
)
go

exec sp_addextendedproperty 'MS_Description', '库存明细表', 'SCHEMA', 'dbo', 'TABLE', 'inventoryTable'
go

exec sp_addextendedproperty 'MS_Description', '库存商品ID', 'SCHEMA', 'dbo', 'TABLE', 'inventoryTable', 'COLUMN', 'cID'
go

exec sp_addextendedproperty 'MS_Description', '库存商品名称', 'SCHEMA', 'dbo', 'TABLE', 'inventoryTable', 'COLUMN', 'cName'
go

exec sp_addextendedproperty 'MS_Description', '库存商品单位数量', 'SCHEMA', 'dbo', 'TABLE', 'inventoryTable', 'COLUMN',
     'cQuantity'
go

exec sp_addextendedproperty 'MS_Description', '库存信息自动更新日期时间', 'SCHEMA', 'dbo', 'TABLE', 'inventoryTable', 'COLUMN',
     'updateDatetime'
go

create unique index inventoryTable_cName_uindex
    on inventoryTable (cName)
go

/* =========创建商品预入库触发器============= */

create trigger insert_inventory
    on purchaseOrder
    after insert
    as
    begin
        if (select cName from inserted) not in (select cName from inventoryTable)
        begin
            insert into inventoryTable(cName, cQuantity)
            select cName, 0 from inserted
        end
    end
go

/* ==========创建入库明细单表============= */

create table [warehouse-inRecords]
(
    wrID          int identity
        constraint [warehouse-inRecords_pk]
            primary key,
    kID           int                        not null
        constraint [warehouse-inRecords_keeperTable_kID_fk]
            references keeperTable,
    poID          int                        not null
        constraint [warehouse-inRecords_purchaseOrder_poID_fk]
            references purchaseOrder,
    pQuantityReal float                      not null,
    wrDatetime    datetime default getdate() not null
)
go

exec sp_addextendedproperty 'MS_Description', '入库单', 'SCHEMA', 'dbo', 'TABLE', 'warehouse-inRecords'
go

exec sp_addextendedproperty 'MS_Description', '入库单编号', 'SCHEMA', 'dbo', 'TABLE', 'warehouse-inRecords', 'COLUMN', 'wrID'
go

exec sp_addextendedproperty 'MS_Description', '库存管理员编号', 'SCHEMA', 'dbo', 'TABLE', 'warehouse-inRecords', 'COLUMN',
     'kID'
go

exec sp_addextendedproperty 'MS_Description', '对应的采购单编号', 'SCHEMA', 'dbo', 'TABLE', 'warehouse-inRecords', 'COLUMN',
     'poID'
go

exec sp_addextendedproperty 'MS_Description', '实际入库数量', 'SCHEMA', 'dbo', 'TABLE', 'warehouse-inRecords', 'COLUMN',
     'pQuantityReal'
go

exec sp_addextendedproperty 'MS_Description', '商品入库日期时间', 'SCHEMA', 'dbo', 'TABLE', 'warehouse-inRecords', 'COLUMN',
     'wrDatetime'
go

create nonclustered index [warehouse-inRecords_poID_nonclustered]
    on [warehouse-inRecords] (poID)
go

/* ==========创建商品确认入库触发器============= */

CREATE trigger update_inventory_in
    on [warehouse-inRecords]
    after insert
    as
    begin
        update inventoryTable
        set cQuantity=cQuantity+(select pQuantityReal from inserted),updateDatetime=getdate()
        where cName=(select cName
                     from inserted i join purchaseOrder po on i.poID=po.poID);
        update purchaseOrder
        set isInWarehouse=1
        where purchaseOrder.poID=(select poID from inserted);
    end
go


/* =========创建销售明细单表========= */

create table salesRecords
(
    srID          int identity
        constraint salesRecords_pk
            primary key,
    sID           int                        not null
        constraint salesRecords_salesmanTable_sID_fk
            references salesmanTable,
    salesDatetime datetime default getdate() not null,
    cID           int                        not null
        constraint salesRecords_inventoryTable_cID_fk
            references inventoryTable (cID),
    srQuantity    float                      not null,
    srUnitPrice   money                      not null
)
go

exec sp_addextendedproperty 'MS_Description', '销售明细表', 'SCHEMA', 'dbo', 'TABLE', 'salesRecords'
go

exec sp_addextendedproperty 'MS_Description', '销售记录编号', 'SCHEMA', 'dbo', 'TABLE', 'salesRecords', 'COLUMN', 'srID'
go

exec sp_addextendedproperty 'MS_Description', '销售员编号', 'SCHEMA', 'dbo', 'TABLE', 'salesRecords', 'COLUMN', 'sID'
go

exec sp_addextendedproperty 'MS_Description', '销售时间', 'SCHEMA', 'dbo', 'TABLE', 'salesRecords', 'COLUMN',
     'salesDatetime'
go

exec sp_addextendedproperty 'MS_Description', '商品销售单位数量', 'SCHEMA', 'dbo', 'TABLE', 'salesRecords', 'COLUMN',
     'srQuantity'
go

exec sp_addextendedproperty 'MS_Description', '实际销售价格', 'SCHEMA', 'dbo', 'TABLE', 'salesRecords', 'COLUMN',
     'srUnitPrice'
go

create nonclustered index salesRecords_cID_nonclustered
    on salesRecords (cID)
go

/* =========创建商品销售出库触发器========= */

create trigger update_inventory_out
    on salesRecords
    after insert
    as
    begin
        update inventoryTable
        set cQuantity=cQuantity-(select srQuantity from inserted),updateDatetime=getdate()
        where cID=(select cid from inserted)
    end
go


INSERT INTO purchaseOrder(pID, cName, sName, pUnitPrice, pQuantity, pMeasuringUnit)
VALUES (1, '晨光橡皮', '晨光文具', 3.0, 100.0, '块');
INSERT INTO purchaseOrder(pID, cName, sName, pUnitPrice, pQuantity, pMeasuringUnit)
VALUES (1, '猫爪杯', '星巴克', 128.0, 10.0, '个');