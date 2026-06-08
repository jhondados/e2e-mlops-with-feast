"""Feast feature repository definition."""
from feast import FeatureStore, Entity, FeatureView, Field, BigQuerySource
from feast.types import Float64, Int64, String
from datetime import timedelta

store = FeatureStore(repo_path=".")

customer_entity = Entity(name="customer_id", join_keys=["customer_id"])

customer_source = BigQuerySource(name="customer_stats_source",
    table="project.features.customer_daily_stats", timestamp_field="event_timestamp")

customer_features = FeatureView(name="customer_features", entities=[customer_entity],
    ttl=timedelta(days=7), source=customer_source,
    schema=[Field(name="total_spend_90d", dtype=Float64),
            Field(name="order_count_30d", dtype=Int64),
            Field(name="avg_order_value", dtype=Float64),
            Field(name="churn_risk_score", dtype=Float64),
            Field(name="customer_segment", dtype=String)])

def get_online_features(customer_ids: list) -> dict:
    return store.get_online_features(features=["customer_features:total_spend_90d",
        "customer_features:order_count_30d", "customer_features:churn_risk_score"],
        entity_rows=[{"customer_id": cid} for cid in customer_ids]).to_dict()
