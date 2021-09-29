-- SELECT pid FROM pg_stat_activity WHERE datname = 'geoconnections';
-- SELECT pg_terminate_backend (pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'geoconnections';
-- DROP DATABASE geoconnections;
-- DROP DATABASE [IF EXISTS] database_name;
DELETE FROM public.location WHERE id>0 RETURNING *;
DELETE FROM public.person WHERE id>0 RETURNING *;