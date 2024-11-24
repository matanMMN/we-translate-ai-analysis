import { Button } from "@/components/ui/button"
import { Paperclip } from "lucide-react"
import { UseFormReturn } from "react-hook-form"
import { FormField, FormItem, FormControl, FormMessage } from "@/components/ui/form"

interface FileUploadFieldProps {
  form: UseFormReturn
  onOpenModal: () => void
  selectedFileName?: string
}

export function FileUploadField({ form, onOpenModal, selectedFileName }: FileUploadFieldProps) {
  return (
    <FormField
      control={form.control}
      name="referenceFile"
      render={() => (
        <FormItem>
          <FormControl>
            <Button
              type="button"
              variant="outline"
              className="w-full bg-gray-50 border-gray-200 hover:bg-gray-100 hover:text-gray-900"
              onClick={onOpenModal}
            >
              <Paperclip className="w-4 h-4 mr-2" />
              {selectedFileName || "Add reference file"}
            </Button>
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  )
} 