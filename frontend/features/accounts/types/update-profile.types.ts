import { z } from "zod";

import { updateProfileSchema } from "../schemas";

export type ProfileFormValues = z.infer<typeof updateProfileSchema>;
