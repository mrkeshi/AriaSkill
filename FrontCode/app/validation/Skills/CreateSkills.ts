
import * as Yup from 'yup';
import { createFileSchema } from '../createFileSchema ';

export const SkillsSchema = Yup.object({
  icon: createFileSchema({
    required: true,
    maxSizeMB: 2,
    allowedTypes: ['image/jpeg', 'image/png']
  }),
  name: Yup.string().required('نام مهارت الزامی است')
});

export const EditSkillsSchema = Yup.object({
  icon: createFileSchema({
    required: false,
    maxSizeMB: 2,
    allowedTypes: ['image/jpeg', 'image/png']
  }),
  name: Yup.string().required('نام مهارت الزامی است')
});

