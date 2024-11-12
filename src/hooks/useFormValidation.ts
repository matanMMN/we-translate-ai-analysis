import { useCallback } from 'react';
import { UseFormReturn } from 'react-hook-form';
import * as z from 'zod';

export const useFormValidation = (form: UseFormReturn<any>, schema?: z.ZodSchema) => {
  const validateField = useCallback(async (fieldName: string, value: any) => {

    await form.trigger(fieldName);

    if (schema) {
      try {
        const fieldSchema = (schema as any).shape[fieldName];
        if (fieldSchema) {
          await fieldSchema.parseAsync(value);
        }
      } catch (error) {
        console.error(error)
        return false;
      }
    }
    return true;
  }, [form, schema]);

  const isFieldValid = useCallback((fieldName: string) => {
    return !form.formState.errors[fieldName];
  }, [form.formState.errors]);

  const getFieldError = useCallback((fieldName: string) => {
    return form.formState.errors[fieldName]?.message as string;
  }, [form.formState.errors]);

  return {
    validateField,
    isFieldValid,
    getFieldError,
    isDirty: form.formState.isDirty,
    isValid: form.formState.isValid,
  };
}; 