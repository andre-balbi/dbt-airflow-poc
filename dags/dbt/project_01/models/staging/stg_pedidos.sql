{{ config(
    materialized='incremental'
) }}

with source as (
    select
    *
    from {{ source('ecommerce','pedidos') }}
)

select
*
from source

{% if is_incremental() %}
    where data_pedido >= (select max(data_pedido) from {{ this }})
{% endif %}