def test_required_dependencies_import():
    from dbt.cli.main import dbtRunner
    from google.cloud import bigquery, storage

    assert dbtRunner is not None
    assert bigquery is not None
    assert storage is not None