APP_NAME := $(shell python metadata.py name)
APP_VERSION := $(shell python metadata.py version)
IMAGE_NAME := demsking/$(APP_NAME)

# Start the development environment using tmuxinator
shell:
	tmuxinator

install:
	poetry install

up: build/requirements.txt
	docker compose up --build -d --remove-orphans

restart:
	docker compose restart

watch: build/requirements.txt
	docker compose watch server

down:
	docker compose down

config:
	docker compose config

logs:
	docker compose logs -f

ps:
	docker compose ps

stats:
	docker compose stats

gen-tests:
	python gen.py http://localhost:26303/api/openapi.json
	pre-commit run double-quote-string-fixer

test: gen-tests
	pytest --ignore=clients -vv

coverage: gen-tests
	pytest --ignore=clients --cov=vikela

coverage-html: gen-tests
	pytest --ignore=clients --cov=vikela --cov-report=html

.PHONY: clients
clients:
	mkdir -p clients/dart
	mkdir -p clients/python
	curl -o clients/spec.yaml http://localhost:26303/openapi.json

	docker run -it --rm \
	  -v $(PWD):/local \
	  -w /local \
	openapitools/openapi-generator-cli \
	  generate \
	    -i /local/clients/spec.yaml \
	    -g dart \
	    --git-host gitlab.com \
	    --git-repo-id vikela \
	    --git-user-id demsking \
	    --package-name '$(APP_NAME)_client' \
	    --http-user-agent '$(APP_NAME)/{packageVersion}' \
	    -o /local/clients/dart

	docker run -it --rm \
	  -v $(PWD):/local \
	  -e PYTHON_POST_PROCESS_FILE="/usr/local/bin/yapf -i" \
	  -e PYTHONPATH=/local \
	  -w /local \
	openapitools/openapi-generator-cli \
	  generate \
	    -i /local/clients/spec.yaml \
	    -g python \
	    --git-host gitlab.com \
	    --git-repo-id vikela \
	    --git-user-id demsking \
	    --package-name '$(APP_NAME)_client' \
	    -o /local/clients/python

# See https://github.com/FiloSottile/mkcert
certificate: deployment/traefik/certs/$(DOMAIN)+1.pem
	mkdir -p deployment/traefik/certs
	cd deployment/traefik/certs && mkcert $(DOMAIN) *.$(DOMAIN)

couchdb-authtoken:
	@echo -n $(COUCHDB_USER) | openssl dgst -sha256 -hmac $(COUCHDB_SECRET)

encoded-jwt-secret:
	@echo -n "$(JWT_SECRET_KEY)" | base64

open-couchdb-ui:
	open http://localhost:25984/_utils

open-vikela-docs:
	open http://localhost:26303/docs

lint:
	pre-commit run --all-files

fix:
	ruff check . --fix

# Show outdated dependencies using poetry
outdated:
	poetry show --outdated

update:
	poetry -C python update
	devbox update
	pre-commit autoupdate

clean:
	rm -rf dist/ /tmp/$(APP_NAME)

#
## Packaging
package: clean
	mkdir -p /tmp/$(APP_NAME)/vikela_models/ dist/
	sed 's/__VERSION__/$(APP_VERSION)/g' pyproject-models.toml > /tmp/$(APP_NAME)/pyproject.toml
	cp LICENSE /tmp/$(APP_NAME)/
	cp README-MODELS.md /tmp/$(APP_NAME)/README.md
	cp -r vikela/models/* /tmp/$(APP_NAME)/vikela_models/
	cd /tmp/$(APP_NAME) && poetry build
	twine check /tmp/$(APP_NAME)/dist/*
	cp /tmp/$(APP_NAME)/dist/* dist/

publish-package: package
	twine upload --verbose -r testpypi dist/*

build/requirements.txt: pyproject.toml poetry.lock
	mkdir -p build/
	poetry export --only=main --without-hashes -f requirements.txt -o $@

image: build/requirements.txt
	docker build . \
	  --progress plain \
	  --tag $(IMAGE_NAME):$(APP_VERSION) \
	  --tag $(IMAGE_NAME):latest \
	  --label "org.opencontainers.image.title=$(APP_NAME)" \
	  --label "org.opencontainers.image.description=$(shell python metadata.py description)" \
	  --label "org.opencontainers.image.version=$(APP_VERSION)" \
	  --label "org.opencontainers.image.revision=$(shell git rev-parse HEAD)" \
	  --label "org.opencontainers.image.authors=$(shell python metadata.py authors)" \
	  --label "org.opencontainers.image.created=$(shell date --rfc-3339=seconds)" \
	  --label "org.opencontainers.image.source=$(shell python metadata.py repository)" \
	  --label "org.opencontainers.image.url=$(shell python metadata.py repository)" \
	  --label "org.opencontainers.image.documentation=$(shell python metadata.py documentation)" \
	  --label "org.opencontainers.image.vendor=Vikela" \
	  --label "org.opencontainers.image.licenses=$(shell python metadata.py license)"

publish: image
	git commit pyproject.toml -m "Release $(APP_VERSION)"
	git tag v$(APP_VERSION)
	git push --tags origin main
	$(MAKE) publish-package
	docker push $(IMAGE_NAME):$(APP_VERSION)
	docker push $(IMAGE_NAME):latest
