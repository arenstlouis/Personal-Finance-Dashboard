# 1. Use Node image
FROM node:20-slim

# 2. Set working directory
WORKDIR /app

# 3. Install dependencies (copying these first speeds up future builds)
COPY package*.json ./
RUN npm install

# 4. Copy the code
COPY . .

# 5. Expose the Vite port
EXPOSE 5173

# 6. Start Vite (the --host flag is required to allow external access)
CMD ["npm", "run", "dev", "--", "--host"]
