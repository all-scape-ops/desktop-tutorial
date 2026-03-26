import { useRef, useState, useCallback } from 'react';
import { Upload, ImageIcon } from 'lucide-react';
import { motion } from 'motion/react';

interface Props {
  onUpload: (base64: string, mimeType: string, preview: string) => void;
}

export default function StepUpload({ onUpload }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const processFile = useCallback(
    (file: File) => {
      if (!file.type.startsWith('image/')) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        const dataUrl = e.target?.result as string;
        const base64 = dataUrl.split(',')[1];
        const preview = dataUrl;
        onUpload(base64, file.type, preview);
      };
      reader.readAsDataURL(file);
    },
    [onUpload],
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) processFile(file);
    },
    [processFile],
  );

  return (
    <div className="flex flex-col items-center gap-8">
      <div className="text-center space-y-3">
        <h2 className="text-3xl font-semibold tracking-tight" style={{ color: '#141414' }}>
          Upload your room
        </h2>
        <p className="text-base text-neutral-500 max-w-md">
          Share a photo of your living room, bedroom, or kitchen — our system handles the rest.
        </p>
      </div>

      <motion.div
        whileHover={{ scale: 1.01 }}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`relative w-full max-w-lg h-64 rounded-2xl border-2 border-dashed cursor-pointer flex flex-col items-center justify-center gap-4 transition-colors
          ${dragging ? 'border-neutral-700 bg-neutral-100' : 'border-neutral-300 bg-white hover:border-neutral-500'}`}
      >
        <div className="flex items-center justify-center w-14 h-14 rounded-full bg-neutral-100">
          <Upload className="w-6 h-6 text-neutral-500" />
        </div>
        <div className="text-center">
          <p className="font-medium text-neutral-700">Drop your photo here</p>
          <p className="text-sm text-neutral-400 mt-1">or click to browse — JPG, PNG, WEBP</p>
        </div>
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => { const f = e.target.files?.[0]; if (f) processFile(f); }}
        />
      </motion.div>

      <div className="flex items-center gap-2 text-sm text-neutral-400">
        <ImageIcon className="w-4 h-4" />
        <span>Best results with well-lit, wide-angle room photos</span>
      </div>
    </div>
  );
}
