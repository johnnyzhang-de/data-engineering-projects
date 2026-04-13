drop table if exists raw_orders;
create table raw_orders (
    order_id            text,
    order_line_id       text,
    order_date          text,
    customer_id         text,
    product_id          text,
    vendor_id           text,
    quantity            text,
    unit_price          text,
    discount_amount     text,
    order_status        text,
    source_file_name    text,
    process_datetime    timestamp
);

drop table if exists raw_customers;
create table raw_customers (
    customer_id         text,
    customer_name       text,
    customer_city       text,
    customer_state      text,
    customer_country    text,
    customer_segment    text,
    source_file_name    text,
    process_datetime    timestamp
);

drop table if exists raw_products;
create table raw_products (
    product_id            text,
    product_name          text,
    product_category      text,
    product_subcategory   text,
    vendor_id             text,
    standard_cost         text,
    list_price            text,
    source_file_name      text,
    process_datetime      timestamp
);

drop table if exists raw_vendors;
create table raw_vendors (
    vendor_id           text,
    vendor_name         text,
    vendor_country      text,
    vendor_status       text,
    source_file_name    text,
    process_datetime    timestamp
);

drop table if exists raw_shipments;
create table raw_shipments (
    shipment_id         text,
    order_id            text,
    shipment_date       text,
    shipment_status     text,
    carrier_name        text,
    tracking_number     text,
    shipped_quantity    text,
    source_file_name    text,
    process_datetime    timestamp
);