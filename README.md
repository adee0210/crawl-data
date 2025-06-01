# Football Video Analysis Pipeline

A scalable pipeline for football video analysis using Apache Airflow, designed to crawl and process data from Web, API, YouTube, and Vimeo sources. The pipeline automates data ingestion and processing workflows, with scheduled DAGs running on the 3rd, 13th, and 23rd of each month. It leverages PyTorch for video frame processing and integrates logging with Airflow.

Click on **Use this template** to initialize a new repository.

Suggestions are always welcome!

## 📌 Introduction

### Why you might want to use it:
✅ **Automation**: Automates data crawling and processing with Airflow DAGs.  
✅ **Scalability**: Easily extendable to new data sources and processing tasks.  
✅ **Reusability**: Modular structure with reusable crawlers and processors.  
✅ **Learning Resource**: Well-documented for learning Airflow and video analysis workflows.

### Why you might not want to use it:
❌ **Not for Real-Time**: Designed for scheduled batch processing, not real-time analysis.  
❌ **Dependency on Airflow**: Requires familiarity with Airflow for customization.  
❌ **Basic Implementation**: Crawlers and processors are basic; may need customization for specific use cases.

**Note**: This is a personal project for learning and prototyping.

## Main Technologies
- **Apache Airflow**: Workflow orchestration for scheduling and managing DAGs.
- **PyTorch**: For deep learning-based video frame processing.
- **Requests, PyTube, Vimeo-Downloader**: For crawling data from Web, YouTube, and Vimeo.
- **OpenCV**: For video frame extraction and processing.

## Main Ideas
- **Scheduled Workflows**: DAGs run on the 3rd, 13th, and 23rd of each month.
- **Modular Design**: Separate crawlers and processors for each data source.
- **Logging**: Integrated with Airflow for centralized log management.
- **Extensibility**: Easily add new data sources or processing tasks.

## Project Structure
.
├── .github                   # GitHub Actions workflows (if added later)
│
├── dags                      # Airflow DAGs
│   ├── api_pipeline_dag.py   # DAG for API data fetching
│   ├── vimeo_pipeline_dag.py # DAG for Vimeo video crawling
│   ├── web_pipeline_dag.py   # DAG for web data crawling
│   └── youtube_pipeline_dag.py # DAG for YouTube video crawling and processing
│
├── src                       # Source code
│   ├── crawlers              # Crawler scripts
│   │   ├── api_crawler.py
│   │   ├── vimeo_crawler.py
│   │   ├── web_crawler.py
│   │   └── youtube_crawler.py
│   │
│   ├── processors            # Processing scripts
│   │   └── frame_processor.py
│   │
│   └── utils                 # Utility scripts
│       ├── error_handler.py
│       └── logger.py
│
├── videos                    # Directory for downloaded videos
│
├── airflow                   # Airflow configuration and logs
│   ├── logs                  # Airflow logs
│   └── airflow.cfg           # Airflow configuration
│
├── tests                     # Tests (to be added)
│
├── .dockerignore             # Files ignored by Docker
├── .gitignore                # Files ignored by Git
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Dockerfile for building Airflow image
├── requirements.txt          # Python dependencies
└── README.md
