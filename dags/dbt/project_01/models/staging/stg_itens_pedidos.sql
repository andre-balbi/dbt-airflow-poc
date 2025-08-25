with source as (
    select
    *
    from {{ source('ecommerce','itens_pedidos') }}
)

select
*
from source