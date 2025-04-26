# Folder Structure
data-sync-demos/
├── one_way_periodic/
│   ├── docker-compose.yml  # PostgreSQL + sync app
│   ├── app/
│   │   ├── Dockerfile
│   │   ├── cronjob
│   │   └── sync.py
│   └── init/
│       └── init.sql
├── one_way_realtime/
│   ├── docker-compose.yml
│   ├── source_service/
│   │   ├── Dockerfile
│   │   └── app.py
│   ├── target_service/
│   │   ├── Dockerfile
│   │   └── app.py
├── two_way_periodic/
│   ├── docker-compose.yml
│   ├── sync_service/
│   │   ├── Dockerfile
│   │   ├── cronjob
│   │   └── sync.py
├── two_way_realtime/
│   ├── docker-compose.yml
│   ├── service_a/
│   │   ├── Dockerfile
│   │   └── app.py
│   ├── service_b/
│   │   ├── Dockerfile
│   │   └── app.py
├── README.md

- [one_way_periodic: One-way sync using cron job](one_way_periodic/README.md)
- [one_way_realtime: One-way sync using webhooks](one_way_realtime/README.md)
- [two_way_periodic: Two-way sync using cron job](two_way_periodic/README.md)
- [two_way_realtime: Two-way sync using webhooks](two_way_realtime/README.md)
