from flask import Blueprint
import click
from flask.cli import with_appcontext
import pandas as pd
from .models import db, ClientFamily
from .clients import client_code_name_dict
from .logger import logging

logger = logging.getLogger(__package__)
importer_bp = Blueprint("commands", __name__, cli_group=None)

@importer_bp.cli.command("import")
@click.argument("file_path", required=True)  # , type=click.Path(exists=True))
@click.argument("sheet", required=True, default="Client")
@with_appcontext
def import_data_from_excel(file_path, sheet):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet, skiprows=2, header=1)
    df = df.iloc[:, 1:][df['status'] == 'Active'].fillna(0)
    code_to_name = client_code_name_dict()

    # Iterate over the DataFrame rows
    try:
        for index, row in df.iterrows():
            # Extract the "code" and "family head entity" data
            client_code = row["code"]
            family_head_code = row["family head entity"] # or client_code # NOTE this needed if decided TO store family heads (remove continue)
            if not family_head_code:
                continue
            client_name = code_to_name[client_code]
            family_name = code_to_name[family_head_code]

            # Create a new ClientFamily object
            client_family = ClientFamily(
                client=client_code, family_head=family_head_code, client_name=client_name, family_head_name=family_name
            )

            # Add to the session and commit (in a try-except to handle constraints)
            db.session.add(client_family)
            logger.debug(f'Imported row {index}: {row["code"]}')
        logger.info(f'Successfully imported {index} rows')
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error importing row {index}: (around entity {row['code']}) {e}")
