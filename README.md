# glkernel Service

This projects provides a wrapper around the [glkernel library](https://github.com/cginternals/glkernel).

## Dependencies

The actual dependencies to build and run this project are:

* Docker
* docker-compose

The internally used dependencies are:

* glkernel
* FastAPI

## Setup

```bash
> docker-compose build
> docker-compose up service
```

## Service

The service provides the following endpoints:

* `/image_from_script` - Converts a kernel construction script (a JavaScript source) to a PNG image
* `/image_from_script_file` - Converts a kernel construction script (a JavaScript source file) to a PNG image
* `/image_from_declaration` - Converts a kernel declaration (JSON) to a PNG image
* `/image_from_declaration_file` - Converts a kernel declaration file (JSON file) to a PNG image
* `/image_from_array` - Converts a kernel declaration (JSON) to a PNG image
* `/image_from_array_file` - Converts a kernel declaration file (JSON file) to a PNG image
* `/array_from_script` - Converts a kernel construction script (a JavaScript source) to a JSON kernel declaration
* `/array_from_script_file` - Converts a kernel construction script (a JavaScript source file) to a JSON kernel declaration
* `/array_from_declaration` - Converts a kernel declaration (JSON) to a JSON kernel declaration
* `/array_from_declaration_file` - Converts a kernel declaration (JSON file) to a JSON kernel declaration

For more documentation and immediate testing you can use the generated `/docs` and `/redoc`.
