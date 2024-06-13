FROM node:lts
WORKDIR /app
COPY . .
RUN npm i
CMD ["npm", "run", "start"]