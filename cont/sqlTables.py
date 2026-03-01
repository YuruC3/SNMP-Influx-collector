from sqlalchemy import Table, Column, MetaData, Integer, String, TIMESTAMP, BigInteger, Numeric, text

metadata = MetaData()

idracMeasurement = Table(
    "IDRACmeasurement",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("time_stamp", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False),
    Column("hostname", String(64), nullable=False),

    Column("powerDrawPSU1", Numeric(7, 2)),
    Column("powerDrawPSU2", Numeric(7, 2)),
    Column("powerDrawBoard", Numeric(7, 2)),
    Column("voltagePSU1", Numeric(7, 2)),
    Column("voltagePSU2", Numeric(7, 2)),

    Column("inletTemp", Numeric(5, 2)),
    Column("exhaustTemp", Numeric(5, 2)),
    Column("cpu1Temp", Numeric(5, 2)),
    Column("cpu2Temp", Numeric(5, 2)),

    Column("uptimeS", BigInteger),
    Column("uptimeH", Numeric(8, 3)),
    Column("uptimeD", Numeric(8, 3)),
)