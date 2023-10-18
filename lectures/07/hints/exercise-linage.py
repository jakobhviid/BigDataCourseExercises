# https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/examples/library/lineage_emitter_rest.py
import datahub.emitter.mce_builder as builder
from datahub.emitter.rest_emitter import DatahubRestEmitter

if __name__ == "__main__":
    # Construct a lineage object.
    lineage_mce = builder.make_lineage_mce(
        [
            builder.make_dataset_urn("mysql", "datahub.experiment", "PROD"),  # Upstream
            builder.make_dataset_urn("mysql", "datahub.results", "PROD"),  # Upstream
        ],
        builder.make_dataset_urn("mysql", "datahub.analysis", "PROD"),  # Downstream
    )

    # Create an emitter to the GMS REST API.
    emitter = DatahubRestEmitter("http://localhost:8080")

    # Emit metadata!
    emitter.emit_mce(lineage_mce)
