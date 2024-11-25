import type {NextConfig} from "next";

const nextConfig: NextConfig = {
    output: 'standalone',
    experimental: {
        serverActions: {
            bodySizeLimit: '3mb'
        }
    },
    typescript: {
        ignoreBuildErrors: true,
    },
};

export default nextConfig;
