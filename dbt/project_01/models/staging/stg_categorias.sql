with source as (
    select
    *
    from {{ source('ecommerce','categorias') }}
)

select
*
from source