import pg from 'pg';
const { Pool } = pg;

// Database connection configuration
const pool = new Pool({
    host: 'localhost',
    port: 5432,
    database: 'mvu_app',
    user: 'slate_apps',
    password: 'your_password_here',
});

export const PostgreSQL = () => {
    return {
        query: async (sql: string, params?: any[]) => {
            const client = await pool.connect();
            try {
                const result = await client.query(sql, params);
                return result;
            } finally {
                client.release();
            }
        }
    };
};