FROM node:18-alpine

WORKDIR /app

# Copy package files first
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Expose Vite's development server port
EXPOSE 3000

# Run Vite development server (serves `main.js`)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]