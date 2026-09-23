`timescale 1ns / 1ps
`timescale 1ns / 1ps

module tb_gamma_top();

    logic clk;
    logic rst_n;
    logic [7:0] r_in, g_in, b_in;
    logic [7:0] r_out, g_out, b_out;
    logic done;

    // CHANGE depending on baseline_non_sc or gamma_top 
    baseline_non_sc uut (
        .clk(clk),
        .rst_n(rst_n),
        .r_in(r_in),
        .g_in(g_in),
        .b_in(b_in),
        .r_out(r_out),
        .g_out(g_out),
        .b_out(b_out),
        .done(done)
    );

    initial clk = 0;
    always #5 clk = ~clk; //100MHz

    // CHANGE depending on total pixels (width * height)
    logic [23:0] image_memory [0:65535]; 
    int output_file;
    int i;

    
    initial begin
        rst_n = 0;
        r_in = 8'd0;
        g_in = 8'd0;
        b_in = 8'd0;

        // CHANGE to input hex filepath
        $readmemh("input_image.hex", image_memory);
        output_file = $fopen("output_image.hex", "w");
        
        if (output_file == 0) begin
            $display("Cant open output file");
            $finish;
        end

        #20; // Reset release = start
        rst_n = 1;

        // CHANGE loop to total pixels
        for (i = 0; i < 65536; i++) begin
            // 24bit hex -> r,g,b
            r_in = image_memory[i][23:16];
            g_in = image_memory[i][15:8];
            b_in = image_memory[i][7:0];

            wait(done == 1'b1);
            
            $fdisplay(output_file, "%02h%02h%02h", r_out, g_out, b_out);

            // Next pixel reset
            @(negedge clk);
            rst_n = 0;
            @(negedge clk);
            rst_n = 1;
        end

        $fclose(output_file);
        $display("Finished");
        $finish;
    end

endmodule