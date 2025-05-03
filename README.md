# StreetEasy Scraper Monorepo

<div align="center" style="margin-bottom: 20px">
    <img src="./docs/src/assets/scraper-hero.png" alt="Scraper mascot hero section" height="350px">
</div>

## TODO

### `packages/utils` module

- [x] Logging configuration

### `packages/db` module

- [x] Database enigne, clients, and context managers
- [x] Database models

### `apps/address_scraper` module

- [x] `address_extractor` class
- [x] `address_transformer` class
- [x] Load transformed addresses locally to `/data` for demonstration

### `apps/webhook` module

- [x] POST `/bd-webhook` to take BrightData's webhook payloads
- [x] Update database async jobs with results status to be extracted later in async pipeline

### `apps/streeteasy_scraper/sync_api` module

- [x] `sync_api` module
- [x] `streeteasy_extractor` class via multithreading serp api
- [x] `streeteasy_transformer` class
- [x] Load transformed data to database
- [ ] Dockerfile

### `apps/streeteasy_scraper/async_api` module

- [ ] `async_api` module
- [ ] `job_submitter` class to send jobs to async serp api and initialize jobs in database
- [ ] `job_results_extractor` class to extract job results when ready
- [ ] Use the transformer from sync api to transform results
- [ ] Load transformed data to database
- [ ] Dockerfile

### `notebooks/result_analysis`

- [ ] Analysis finished jobs in a Jupyter notebook
- [ ] Convert notebook into markdown with `nb-convert`

### `docs`

- [ ] Getting started
- [ ] Installation
- [ ] Configuration
- [ ] Guides
