CONTENT_DIR := /opt/stackstorm
PACK_DIR := $(CONTENT_DIR)/packs
PACK := mypack

all: deploy setup register

deploy:
	sudo cp -r . $(PACK_DIR)/$(PACK)

setup:
	st2 run packs.setup_virtualenv packs=$(PACK)

register:
	sudo st2ctl reload --register-all
