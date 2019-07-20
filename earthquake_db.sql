CREATE TABLE earthquake
(
   "lat" numeric(14, 4) NOT NULL,
   "lon" numeric(14, 4) NOT NULL,
   "mag" numeric(12, 1) NOT NULL,
   "time" timestamp without time zone NOT NULL
)
WITH (
   OIDS = FALSE
);

Select *
From earthquake