import * as React from "react"
import * as LabelPrimitive from "@radix-ui/react-label"
import {
    Controller,
    ControllerProps,
    FieldPath,
    FieldValues,
    FormProvider,
    useFormContext,
} from "react-hook-form"

import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"

const ProjectForm = FormProvider

const ProjectFormField = <
    TFieldValues extends FieldValues = FieldValues,
    TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
>({
    ...props
}: ControllerProps<TFieldValues, TName>) => {
    return (
        <Controller
            {...props}
        />
    )
}

const ProjectFormItem = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
    return (
        <div ref={ref} className={cn("space-y-2", className)} {...props} />
    )
})
ProjectFormItem.displayName = "ProjectFormItem"

const ProjectFormLabel = React.forwardRef<
    React.ElementRef<typeof LabelPrimitive.Root>,
    React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root>
>(({ className, ...props }, ref) => {
    return (
        <Label
            ref={ref}
            className={cn("", className)}
            {...props}
        />
    )
})
ProjectFormLabel.displayName = "ProjectFormLabel"

const ProjectFormControl = React.forwardRef<
    HTMLDivElement,
    React.HTMLAttributes<HTMLDivElement>
>(({ children, ...props }, ref) => {
    const { error, formItemId, formDescriptionId, formMessageId }: any = useFormContext()

    return (
        <div
            ref={ref}
            id={formItemId}
            aria-describedby={
                !error
                    ? `${formDescriptionId}`
                    : `${formDescriptionId} ${formMessageId}`
            }
            aria-invalid={!!error}
            {...props}
        >
            {children}
        </div>
    )
})
ProjectFormControl.displayName = "ProjectFormControl"

const ProjectFormMessage = React.forwardRef<
    HTMLParagraphElement,
    React.HTMLAttributes<HTMLParagraphElement>
>(({ className, children, ...props }, ref) => {
    const { error, formMessageId }: any = useFormContext()
    const body = error ? String(error?.message) : children

    if (!body) {
        return null
    }

    return (
        <p
            ref={ref}
            id={formMessageId}
            className={cn("text-sm font-medium text-destructive", className)}
            {...props}
        >
            {body}
        </p>
    )
})
ProjectFormMessage.displayName = "ProjectFormMessage"

export {
    ProjectForm,
    ProjectFormItem,
    ProjectFormLabel,
    ProjectFormControl,
    ProjectFormMessage,
    ProjectFormField,
} 