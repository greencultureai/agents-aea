``` bash
aea create my_aea
```
``` bash
aea add connection fetchai/http:0.1.0
```
``` bash
aea config set vendor.fetchai.connections.http.config.api_spec_path "examples/http_ex/petstore.yaml"
```
``` bash
aea install
```
``` bash
aea scaffold skill http_echo
```