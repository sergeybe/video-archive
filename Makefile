REPOSITORY_USER := sergeybe
VERSION := 0.0.1
SERVICE := django
LATEST_IMAGE := 'video-archive_$(SERVICE):latest'
VERSION_IMAGE = $(subst :latest,:$(VERSION),$(LATEST_IMAGE))

all:
	@echo 'Run "make start" for build Docker images by docker-composer and start them.'

start: build up migrate collectstatic
stop: down

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

destroy:
	docker-compose down -v

migrate:
	docker-compose exec django python manage.py migrate --noinput

collectstatic:
	docker-compose exec django python manage.py collectstatic --noinput

loadfixtures:
	@echo TODO

prune:
	docker system prune

tags:
	docker tag $(LATEST_IMAGE) $(VERSION_IMAGE)
	docker tag $(LATEST_IMAGE) $(REPOSITORY_USER)/$(VERSION_IMAGE)
	docker tag $(LATEST_IMAGE) $(REPOSITORY_USER)/$(LATEST_IMAGE)

push: tags
	docker push $(REPOSITORY_USER)/$(VERSION_IMAGE)
	docker push $(REPOSITORY_USER)/$(LATEST_IMAGE)

.PHONY: build show migrate collectstatic loadfixtures sleep up down start stop destroy prune all
