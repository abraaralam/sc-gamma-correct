`timescale 1ns / 1ps

// takes a pixel's r, g, and b values and produces 256bit stochastic multiplication to output a square gamma corrected pixel
// needs to be reset for each pixel, and holds done flag + value when completed 

module gamma_top(
    input logic clk,
    input logic rst_n,
    input logic [7:0] r_in,
    input logic [7:0] g_in,
    input logic [7:0] b_in,
    output logic [7:0] r_out,
    output logic [7:0] g_out,
    output logic [7:0] b_out,
    output logic done
    );
    
    logic [7:0] lfsr_val;
    
    lfsr_8bit my_lfsr (
        .clk(clk),
        .rst_n(rst_n),
        .lfsr_out(lfsr_val)
    );
    
    logic [7:0] ctr;
    logic r_bit, g_bit, b_bit;
    logic last_r, last_g, last_b;
    logic r_and, b_and, g_and;
    
    sng r_sng (.lfsr_in(lfsr_val), .num_in(r_in), .bitstream(r_bit));
    sng g_sng (.lfsr_in(lfsr_val), .num_in(g_in), .bitstream(g_bit));
    sng b_sng (.lfsr_in(lfsr_val), .num_in(b_in), .bitstream(b_bit));
    
    assign r_and = last_r & r_bit;
    assign g_and = last_g & g_bit;
    assign b_and = last_b & b_bit;
    
    //output registers
    logic [7:0] r_acc, g_acc, b_acc;
    assign r_out = r_acc;
    assign g_out = g_acc;
    assign b_out = b_acc;
    
    // now we have r stream, g stream, and b stream. we need to remmeber last r,g&b bit as the clock changes
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin 
            last_r <= 1'b0;
            last_g <= 1'b0;
            last_b <= 1'b0;
            ctr <= 8'd0;
            done <= 1'b0;
            r_acc <= 8'b0;
            g_acc <= 8'b0;
            b_acc <= 8'b0;
        end else begin
            last_r <= r_bit;
            last_g <= g_bit;
            last_b <= b_bit;
            if (ctr == 8'd255) begin
                done <= '1;
            end else begin
                done <= '0;
                ctr <= ctr + 8'd1;
                if (r_and) r_acc <= r_acc + 8'd1;
                if (g_and) g_acc <= g_acc + 8'd1;
                if (b_and) b_acc <= b_acc + 8'd1;
            end
        end
        
    end       
    
    
endmodule
