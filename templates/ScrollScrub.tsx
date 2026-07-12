"use client";
// Scroll-scrubbed frame sequence (design-law scrollytelling primitive).
// Frames come from: python mcp/assets/assets.py frames <video.mp4> 24
// Usage: <ScrollScrub dir="/frames/hero" count={120} className="h-[300vh]" />
// Honor prefers-reduced-motion at the call site: render a poster <img> instead.
import { useEffect, useRef } from "react";

export function ScrollScrub({ dir, count, pad = 4, className = "" }: {
  dir: string; count: number; pad?: number; className?: string;
}) {
  const wrap = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const imgs = Array.from({ length: count }, (_, i) => {
      const img = new Image();
      img.src = `${dir}/frame_${String(i + 1).padStart(pad, "0")}.webp`;
      return img;
    });
    const ctx = canvas.current!.getContext("2d")!;
    let current = -1;
    const draw = (i: number) => {
      const img = imgs[i];
      if (!img?.complete || i === current) return;
      current = i;
      canvas.current!.width = img.naturalWidth;
      canvas.current!.height = img.naturalHeight;
      ctx.drawImage(img, 0, 0);
    };
    imgs[0].onload = () => draw(0);
    const onScroll = () => {
      const el = wrap.current!;
      const p = -el.getBoundingClientRect().top / (el.scrollHeight - innerHeight);
      draw(Math.min(count - 1, Math.max(0, Math.round(p * (count - 1)))));
    };
    addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    return () => removeEventListener("scroll", onScroll);
  }, [dir, count, pad]);

  return (
    <div ref={wrap} className={className}>
      <canvas ref={canvas} className="sticky top-0 h-screen w-full object-cover" />
    </div>
  );
}
