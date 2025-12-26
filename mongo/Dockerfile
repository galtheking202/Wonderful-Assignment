# Use official MongoDB image
FROM mongo:7.0

# Copy any initialization scripts
COPY init-mongo.js /docker-entrypoint-initdb.d/

# Expose MongoDB default port
EXPOSE 27017
