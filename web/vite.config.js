import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
            'assets': '@/assets',
            'components': '@/components',
            'views': '@/views',
        }
    },
    define: {
        'process.env': process.env
    },
    build: {
        target: 'modules',
        outDir: '../static',
        assetsDir: 'assets'
    },
    server: {
        cors: true,
        open: true,
        port: 8080,
        proxy: {
            '^/api': {
                target: 'http://127.0.0.1:80',
                changeOrigin: true,
            },
            '^/uploads': {
                target: 'http://127.0.0.1:80',
                changeOrigin: true
            }
        }
    }
})
