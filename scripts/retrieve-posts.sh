#!/bin/bash
# Retrieves posts from social media sources
docker-compose exec backend python manage.py retrieve_reddit_comments \
&& docker-compose exec backend python manage.py retrieve_reddit_posts \
&& docker-compose exec backend python manage.py retrieve_twitter_tweets