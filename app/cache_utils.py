from app.redis_client import redis_client


async def invalidate_product_list_cache():
    await redis_client.delete("products:all")


async def invalidate_product_detail_cache(product_id: int):
    await redis_client.delete(f"products:{product_id}")


async def invalidate_product_caches(product_ids: list[int] | None = None):
    await invalidate_product_list_cache()

    if product_ids:
        for product_id in product_ids:
            await invalidate_product_detail_cache(product_id)