FROM postgres:13
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_USER=admin
ENV POSTGRES_DB=keywords 

COPY create_base.sql /docker-entrypoint-initdb.d/create_base.sql