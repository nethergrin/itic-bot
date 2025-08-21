# Stage 1: build the React app
FROM node:23-slim AS build
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Stage 2: serve with Nginx
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]