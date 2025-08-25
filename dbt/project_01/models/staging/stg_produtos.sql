with source as (
    select
    *
    from {{ source('ecommerce','produtos') }}
)

select
*
from source