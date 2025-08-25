with source as (
    select
    *
    from {{ source('ecommerce','pagamentos') }}
)

select
*
from source