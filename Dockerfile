# 1. Use a small official Node image
FROM node:22-alpine

# 2. Create app directory
WORKDIR /app

# 3. Install dependencies first (cache layer)
COPY package*.json ./
RUN npm install --omit=dev

# 4. Copy the rest of the backend code
COPY . .

# 5. Expose backend port
EXPOSE 5000

# 6. Start the server
CMD ["npm", "start"]
