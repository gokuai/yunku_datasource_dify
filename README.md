# Gokuai Yunku Datasource Plugin

**Author**: gokuai
**Version**: 0.0.1
**Type**: datasource

## Introduction

This plugin integrates with Gokuai Yunku,  It supports browsing files and folders  and downloading files directly for use in platforms like Dify.

## Features

- **Download Files**: Retrieve files
- **Folder Navigation**: Support for hierarchical folder structure browsing
- **Pagination Support**: Efficiently handle large numbers of files with pagination

## Setup

### Prerequisites

Before using this plugin, you need:
1. An gokuai yunku account with active gokuai yunku
2. The files you want to access
3. gokuai yunku credentials with appropriate permissions

### Developer

​	The address of the authorization document is at [gokuai develpoer](https://developer.gokuai.com/grant/library.html)

## Usage

### Browsing Files

The plugin provides an online drive interface for browsing R2 content:

1. **Navigate Folders**: Click on folders to browse their contents
2. **Pagination**: Use pagination controls for buckets with many files

### Downloading Files

To download a file:
1. Browse to the desired file
2. Select the file for download
3. The plugin retrieves the file content and metadata


## Security Considerations

- **Credentials**: Store your gokuai yunku credentials securely and never share them
- **Permissions**: Use the principle of least privilege - grant only necessary permissions

## Troubleshooting

### Common Issues

1. **"Credentials not found" error**:
   - Verify that Access Key ID and Secret Access Key are correctly configured

## Privacy

Please refer to the [Privacy Policy](PRIVACY.md) for information on how your data is handled when using this plugin.

## Support

For issues or questions:

- Repository: [https://github.com/gokuai/yunku_datasource_dify](https://github.com/gokuai/yunku_datasource_dify)

Last updated: Novmber 2025

