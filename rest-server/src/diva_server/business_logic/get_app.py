import json
from pathlib import Path
from ..util import dry_run, get_logger, temp_dir

(debug, info, warning, _, _) = get_logger(__name__)


def main(id: str):
    info(f'getting application status:')
    info(f'id = {id}')

    debug('looking for app metadata...')
    meta = Path(temp_dir(), id, '_meta.json')

    if not meta.exists():
        return "app data not found", 404

    with open(meta, mode='r') as f:
        metadata = json.load(f)
        # data = {
        #     "id": "day_trader",
        #     "name": "Day Trader (WAS)",
        #     "source": {
        #         "github_url": "https://github.com/WASdev/sample.daytrader7.git"
        #     },
        #     "status": "available"
        # }
        return metadata, 200


def get_db(id: str):
    if dry_run():
        warning(
            'dry run flag is true. skips actual business logic and returns dummy response.')
        return {
            "/app": [
                "accountprofileejb",
                "orderejb",
                "holdingejb",
                "accountejb",
                "quoteejb",
                "keygenejb"
            ]
        }

    info(f'getting database info of an application:')
    info(f'id = {id}')

    debug('looking for app metadata...')
    meta = Path(temp_dir(), id, '_meta.json')

    if not meta.exists():
        return "app data not found", 404

    out_path = Path(temp_dir(), id, 'database.json')
    with open(out_path) as f:
        return json.load(f)


def get_tx(id: str):
    info(f'getting tx info of an application:')
    info(f'id = {id}')

    debug('looking for app metadata...')
    meta = Path(temp_dir(), id, '_meta.json')

    if not meta.exists():
        return "app data not found", 404

    out_path = Path(temp_dir(), id, 'transaction.json')
    with open(out_path) as f:
        return json.load(f)
