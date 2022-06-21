const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports =
{
    entry: {
        dashboard_vendor: "./static/js/vendor.js",
        dashboard_main: "./static/js/index.js",
        website_vendor: "./website/static/js/vendor.js",
        website_main: "./website/static/js/index.js",
    },
    output: {
        filename: "js/[name].[contenthash].bundle.js",
        path: path.resolve(__dirname, "dist"),
    },
    plugins: [
        new HtmlWebpackPlugin({
            template:
                "./accounts/templates/accounts/base_template.html",
            filename: "templates/accounts/base_template.html",
            publicPath: "/static/",
            inject: "body",
            chunks: ["website_vendor", "website_main"],
        }),
        new HtmlWebpackPlugin({
            template:
                "./dashboard/templates/dashboard/base_template.html",
            filename: "templates/dashboard/base_template.html",
            publicPath: "/static/",
            inject: "body",
            chunks: ["dashboard_vendor", "dashboard_main"],
        }),
        new HtmlWebpackPlugin({
            template:
                "./website/templates/website/base_template.html",
            filename: "templates/website/base_template.html",
            publicPath: "/static/",
            chunks: ["website_vendor", "website_main"],
            inject: "body"
        }),
        new HtmlWebpackPlugin({
            template:
                "./website/templates/website/website_dashboard.html",
            filename: "templates/website/website_dashboard.html",
            publicPath: "/static/",
            chunks: ["website_vendor", "website_main"],
            inject: "body"
        }),
        new CleanWebpackPlugin(),
    ],
}