import { PostgreSQL } from '$lib/database';

interface IDepartment {
	department_id: number;
	department_name: string;
}

interface ValidationError {
	error: string;
}

export type { IDepartment, ValidationError };

export const Department = () => {
	const api = {
		generateObject: (row: any): IDepartment => {
			const object: IDepartment = {
				department_id: row.department_id,
				department_name: row.department_name
			};
			return object;
		},
		getAll: async (): Promise<Array<IDepartment>> => {
			const results: IDepartment[] = [];
			const sql = `select * from data.department order by department_name`;
			const response = await PostgreSQL().query(sql);
			for (const row of response.rows) {
				const record = api.generateObject(row);
				results.push(record);
			}

			return results;
		},
		getSingle: async (id: number): Promise<IDepartment | void> => {
			const sql = `select * from data.department where department_id = $1`;
			const response = await PostgreSQL().query(sql, [id]);
			for (const row of response.rows) {
				const record = api.generateObject(row);
				return record;
			}

			
		},
		update: async (record: IDepartment): Promise<IDepartment | ValidationError> => {
            if (record.department_name.trim() === ''){
                return {error:`Please provide a department name`}
            }
            const sql = `update data.department set department_name = $1 where department_id = $2 returning *`;
			const response = await PostgreSQL().query(sql, [record.department_name, record.department_id]);
            
            if(!response.rowCount){
                throw new Error('Unable to update record')
            }

            return api.generateObject(response.rows[0])
        },


		insert: async  (record: IDepartment): Promise<IDepartment | ValidationError> => {
            if (record.department_name.trim() === ''){
                return {error:`Please provide a department name`}
            }
            const sql = `insert into data.department (department_name) values ($1) returning *`;
			const response = await PostgreSQL().query(sql, [record.department_name]);
            
            if(!response.rowCount){
                throw new Error('Unable to update record')
            }

            return api.generateObject(response.rows[0])
        },
		delete: async (id: number): Promise<void> => {
            await PostgreSQL().query('delete from data.department where department_id = $1' [id])
        }
	};
	return api;
};
