#!/usr/bin/env python

import os

gems = ["bundler",
        "multi_json",
        "rake",
        "rack",
        "rspec-core",
        "diff-lcs",
        "json",
        "rspec-expectations",
        "rspec-mocks",
        "mime-types",
        "activesupport",
        "rspec",
        "i18n",
        "thor",
        "tzinfo",
        "rspec-support",
        "nokogiri",
        "builder",
        "tilt",
        "minitest",
        "activemodel",
        "activerecord",
        "rails",
        "sass",
        "thread_safe",
        "erubis",
        "actionpack",
        "rack-test",
        "actionmailer",
        "arel",
        "mail",
        "railties",
        "sprockets",
        "rubygems-update"]

for gem in gems:
    print "Fetching "+gem
    os.system("gem fetch "+gem)
    
os.system("gem unpack *.gem")
