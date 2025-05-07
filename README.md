# StreetEasy Scraper

[![Documentation](https://img.shields.io/badge/Documentation-Link-blue)](https://nedhmn.github.io/streeteasy-scraper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

The **StreetEasy Scraper** is a flexible and scalable data collection monorepo designed to scrape property listing information from StreetEasy.com and manage the scraping process using a PostgreSQL database.

<div align="center" style="margin-bottom: 20px">
    <img src="./docs/src/assets/scraper-hero.png" alt="Scraper mascot hero section" height="350px">
</div>

## ✨ Features

- **Monorepo Structure:** Organized as a **monorepo** using `uv` workspaces, facilitating shared code (packages) and independent applications.
- **Flexible Scraping Methods:** Choose between a simple **synchronous** multi-threaded approach or a scalable **asynchronous** workflow leveraging BrightData callbacks.
- **BrightData Integration:** Seamlessly integrates with BrightData's Web Unlocker for handling complex scraping challenges at scale.
- **Efficient Asynchronous Workflow:** Utilizes a dedicated **FastAPI webhook** and background processing for reliable callback handling and data processing.
- **Secure Webhook Exposure:** Employs **Cloudflared tunnels** for secure and reliable public exposure of the webhook without exposing your network directly.
- **Enhanced Security:** Includes options for implementing **Cloudflare IP whitelisting and SSL/TLS encryption** for the webhook endpoint.
- **Robust Data Management:** Stores and manages addresses to be scraped and the collected data in a **PostgreSQL** database.
- **Simplified Deployment:** Easily deploy and manage all project services using **Docker Compose** with distinct profiles for synchronous and asynchronous modes.
- **Automated Address Seeding:** Includes a tool to seed the database with initial addresses from nyc.gov.

## 🚀 Getting Started (Synchronous Quickstart)

This quickstart will get the simpler synchronous scraping profile up and running using Docker.

### Prerequisites

You will need **Docker** and **Docker Compose** installed on your machine.

### Clone the Repository

```bash
git clone https://github.com/nedhmn/streeteasy-scraper.git
cd streeteasy-scraper
```

### Configure Environmental Variables

Copy the `.env.example` file to `.env` and fill in the required values. At a minimum, you'll need to configure the database credentials and basic BrightData Web Unlocker proxy details for the synchronous profile.

```bash
cp .env.example .env
# Edit the .env file with your credentials
```

Refer to the **[Configuration section in the documentation](https://nedhmn.github.io/streeteasy-scraper/getting-started/configuration/)** for detailed instructions on all environment variables.

### Build and Run with Docker Compose (Sync Profile)

```bash
docker-compose --profile sync up --build
```

This command will build the necessary images, start the PostgreSQL database, run the prestart script (which includes initial address seeding), and launch the synchronous scraper.

For detailed information on the asynchronous setup, system architecture, providing addresses, and accessing scraped data, please refer to the **[full documentation](https://nedhmn.github.io/streeteasy-scraper/)**.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
