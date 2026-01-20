import { Department } from '$lib/server/department';
import type { PageServerLoad} from './$types';

export const load: PageServerLoad = async () => {
    const departments = await Department().getAll()

    return {
        departments
    }

}


