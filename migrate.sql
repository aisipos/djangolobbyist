-- Run ./manage.py syncdb to setup django_lobbyist DB
-- Setup lobbyist DB from http://data.sunlightlabs.com/sunlightapi/api_lobbyists.sql.gz
use django_lobbyist;

-- Setup mainsite_client (69160 unique clients from 418898 rows in lobbyist.filing, but there are 5249 unique client_senate_id
insert into mainsite_client (
    client_senate_id,
    client_name,
    client_country,
    client_state,
    client_ppb_country,
    client_ppb_state,
    client_description,
    client_contact_firstname,
    client_contact_middlename,
    client_contact_lastname,
    client_contact_suffix,
    client_raw_contact_name 
) select 
    client_senate_id,
    client_name,
    client_country,
    client_state,
    client_ppb_country,
    client_ppb_state,
    client_description,
    client_contact_firstname,
    client_contact_middlename,
    client_contact_lastname,
    client_contact_suffix,
    client_raw_contact_name 
from 
    lobbyist.lobbyists_filing
where
    client_senate_id is not NULL
group by 
    client_senate_id,
    client_name,
    client_country,
    client_state,
    client_ppb_country,
    client_ppb_state,
    client_description,
    client_contact_firstname,
    client_contact_middlename,
    client_contact_lastname,
    client_contact_suffix,
    client_raw_contact_name ;

-- Use this query to see the variation in "clients"
 -- select 
 --    client_senate_id,
 --    count(client_senate_id),
 --    count(distinct(client_name)),
 --    count(distinct(client_country)),
 --    count(distinct(client_state)),
 --    count(distinct(client_ppb_country)),
 --    count(distinct(client_ppb_state)),
 --    count(distinct(client_description)),
 --    count(distinct(client_contact_firstname)),
 --    count(distinct(client_contact_middlename)),
 --    count(distinct(client_contact_lastname)),
 --    count(distinct(client_contact_suffix)),
 --    count(distinct(client_raw_contact_name))
 -- from 
 --    lobbyist.lobbyists_filing
 --    group by client_senate_id
 
-- Setup registrants
insert into mainsite_registrant (
    registrant_senate_id,
    registrant_name,
    registrant_description,
    registrant_address,
    registrant_country,
    registrant_ppb_country
)
select
    registrant_senate_id,
    registrant_name,
    registrant_description,
    registrant_address,
    registrant_country,
    registrant_ppb_country
from 
    lobbyist.lobbyists_filing
where
    registrant_senate_id is not null
group by
    registrant_senate_id,
    registrant_name,
    registrant_description,
    registrant_address,
    registrant_country,
    registrant_ppb_country;

insert into mainsite_filing (
    filing_id,
    filing_period,
    filing_date,
    filing_amount,
    filing_year,
    filing_type,
    client_senate_id_id,
    registrant_senate_id_id,
)
select
    filing_id,
    filing_period,
    filing_date,
    filing_amount,
    filing_year,
    filing_type,
