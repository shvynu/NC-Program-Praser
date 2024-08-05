# NC Program Data Extraction Tool

## Overview

This repository contains a project developed to automate the extraction and storage of data points from NC (Numerical Control) programs used in CNC (Computer Numerical Control) machinery. The tool parses NC programs, transforms the extracted data into a structured format, and stores it in a SQL database, reducing manual data entry and enabling integration with analytics tools.

## Features

- **Automated Data Extraction**: Efficiently extracts key data points from NC programs.
- **Data Transformation**: Converts extracted data into a SQL-compatible format.
- **SQL Database Integration**: Stores data points in a SQL database for easy retrieval and analysis.
- **Analytics Integration**: Supports integration with analytics tools like Tableau and Qlik Sense.

## Getting Started

### Prerequisites

- Python 3.x
- SQL Database (e.g., MySQL, PostgreSQL)
- Required Python libraries (see `requirements.txt`)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/nc-program-data-extraction.git
   cd nc-program-data-extraction
