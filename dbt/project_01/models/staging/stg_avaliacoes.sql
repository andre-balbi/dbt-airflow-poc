with source as (
    select
    *
    from {{ source('ecommerce','avaliacoes') }}
)

select
*
from source