FROM node:20

# Install curl for container healthchecks
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY baml_src ./baml_src

# If you want to pin to a specific version (which we recommend):
# RUN npm install -g @boundaryml/baml@<VERSION>
RUN npm install -g @boundaryml/baml

EXPOSE 2024

# Point CLI to the source directory explicitly
CMD baml-cli serve --port 2024 --from /app/baml_src