with source as (
    select
    *
    from {{ source('ecommerce','carrinho') }}
)

select
*
from source